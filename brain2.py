
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import math
from ultralytics import YOLO


@st.cache_resource
def cache_model() :
    return YOLO("best.pt")


st.title("ScoliAware : Scoliosis Severity Calculator")
option = st.radio("Choose:" , ("Upload image of X-Ray", "Take picture of X-Ray (spine)"))
img_file = None
if option == "Upload image of X-Ray":
    img_file = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
else:
    img_file = st.camera_input("Take a picture of the X-ray")


if img_file:
    
    st.image(img_file, caption="SPINAL PICTURE:", use_column_width=True)
    img = Image.open(img_file)
    width,height = img.size
    coords = streamlit_image_coordinates(img)
    st.write("MANUAL: Click the MOST TILTED VERTEBRAE at the top and bottom of the curve.")


    if "points" not in st.session_state:      
        st.session_state["points"] = []    # seshstate = {points: }

    if coords and len(st.session_state["points"]) <2:
            point = coords["x"], coords["y"]
            if point not in st.session_state["points"] :
                st.session_state["points"].append(point)
                st.success(f"Point {len(st.session_state.points)} recorded: {point}")
                st.rerun()

    if len(st.session_state["points"]) == 2 :
        (x1,y1),(x2,y2) = st.session_state["points"][0], st.session_state["points"][1]
        st.success("2 points successfully recorded")
        if x2-x1 != 0 :
            x = x2 - x1
            y = y2 - y1
        
            angle_radians = math.atan2(y, x)   
            cobb_angle = abs(math.degrees(angle_radians))
            cobb_angle = min(cobb_angle, 180 - cobb_angle)  

            st.subheader(f"Approximate Cobb Angle:{abs(cobb_angle):.1f}")


    st.divider()


 # YOLO IMPLEMENTATION
    if st.button("Run AI Automated Analysis"):
        with st.spinner("AI is analyzing vertebrae..."):
            model = cache_model()
            results = model(img)
            result = results[0]

        all_vert_coords = []
        for i in result.boxes:
            num_id = int(i.cls[0])
            name = result.names[num_id]
            if name == "Vertebra":
                x, y, w, h = i.xywh[0]  # getting x/y center of box to append as 1 coord
                all_vert_coords.append((float(x), float(y)))

        
        if len(all_vert_coords) < 3:
            st.subheader("Need at least 3 vertebrae for curve analysis.")
        else:
            # sort w/ y coord
            all_vert_coords.sort(key=lambda p: p[1])

            angles = []
            for i in range(len(all_vert_coords) - 1):
                p1 = all_vert_coords[i]
                p2 = all_vert_coords[i+1]
                
                # cal angles btw all vertebrae (in grps of 2)
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                angle = math.degrees(math.atan2(dx, dy)) # Tilt from vertical
                angles.append(angle)

        
            max_right = max(angles) if max(angles) > 0 else 0
            max_left = min(angles) if min(angles) < 0 else 0
            
            ai_cobb_estimate = max_right - max_left
            if ai_cobb_estimate > 90 :
                ai_cobb_estimate = 180 - ai_cobb_estimate

            st.subheader(f"AI-estimated Cobb Angle: {ai_cobb_estimate:.1f}°")  
            if ai_cobb_estimate < 5:
                st.write("Severity: Normal / Very Mild")
            elif ai_cobb_estimate < 15:
                st.write("Severity: Mild")
            elif ai_cobb_estimate < 40:
                st.write("Severity: Moderate")
            else:
                st.write("Severity: Severe")

if st.button("Reset Points"):
    st.session_state["points"] = []
    st.rerun()

st.caption("DISCLAIMER⚠️: This is a rough estimate for awareness only. Please consult a professional.")
st.caption("MAY NOT PROVIDE ACCURATE")

