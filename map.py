import folium
import pandas as pd

# Load data from CSV
df = pd.read_csv("allLocation.csv")  # your CSV file name

# Create base map
m = folium.Map(location=[12.9086641, 77.6341012], zoom_start=12, tiles="CartoDB Voyager")

# Loop through all rows in CSV
for i, row in df.iterrows():
    lat, lon = row['lat'], row['lon']
    name = row['name']
    loc = row['loc']
    image = row['image']
    is_selected = str(row.get('is_selected', '')).strip().upper() == "TRUE"

    # Choose icon
    icon_size = (80, 50) if (lat == 12.9086641) else (15, 20)
    icon_image = image if (lat == 12.9086641) else ("we.png")
    icon = folium.CustomIcon(icon_image=icon_image, icon_size=icon_size)

    # Tooltip
    tooltip = f"{name}, <br>Right Work Decor" if is_selected else None

    # Popup
    popup_html = f"""
    <div style="text-align: center; padding: 10px; font-family: 'Georgia', serif;">
        <img src='{image}' alt='{name}' style='width: 250px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);'><br>
        <div style='font-weight: bold; font-size: 16px; margin-top: 10px; color: #1d4b7f;'>{name}</div>
        <div style='font-size: 14px; color: #555;'>{loc}</div>
    </div>
    """ if is_selected else None
    popup = folium.Popup(popup_html, max_width=250)

    # Add marker
    if is_selected or (lat == 12.9086641) :
        marker = folium.Marker(location=[lat, lon], icon=icon, tooltip=tooltip, popup=popup)
        marker.add_to(m)
    else:
        marker = folium.Marker(location=[lat, lon], icon=icon,)
        marker.add_to(m)


# JavaScript: Save selected project info
selected = df[df['is_selected'] == True]
selected_js = "<script>\nvar selectedProjects = [\n"
for _, row in selected.iterrows():
    selected_js += f"""{{
        lat: {row["lat"]},
        lon: {row["lon"]},
        name: "{row["name"]}",
        image: "{row["image"]}"
    }},"""
selected_js += "\n];\n</script>"
m.get_root().html.add_child(folium.Element(selected_js))



# Add marker metadata for JavaScript
m.get_root().html.add_child(folium.Element(f"""
<script>
    setTimeout(() => {{
    var el = document.getElementsByClassName('leaflet-marker-icon')[{i}];
            el.setAttribute('data-lat', '{lat}');
            el.setAttribute('data-lon', '{lon}');
            el.setAttribute('data-selected', '{str(is_selected).lower()}');
    }}, 100);
</script>
"""))

# Add buttons for UI
m.get_root().html.add_child(folium.Element(f"""
<div id='all-Pro' style='
    position: fixed;
    bottom: 50px; left: 50px;
    width: 180px; height: 30px;
    background-color: white;
    border: 2px solid #1d4b7f;
    box-shadow: 0 0 0 3px #5da2d5;
    z-index: 9999;
    padding: 5px 10px;
    font-size: 12px;
    font-family: Georgia, serif;
    color: #1d4b7f;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
'>
    Locations covered : {len(df) - 1}
</div>
"""))

m.get_root().html.add_child(folium.Element(f"""
<div id='toggle-selected' style='
    position: fixed;
    bottom: 50px; left: 250px;
    width: 170px; height: 30px;
    background-color: white;
    border: 2px solid green;
    box-shadow: 0 0 0 3px lightgreen;
    z-index: 9999;
    padding: 5px 10px;
    font-size: 12px;
    font-family: Georgia, serif;
    color: green;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
'>
    Selected Projects : {len(selected)-1}
</div>
"""))

# JavaScript: Toggle visibility
m.get_root().html.add_child(folium.Element("""
<script>
document.getElementById('toggle-selected').addEventListener('click', function() {
    var markers = document.getElementsByClassName('leaflet-marker-icon');
    for (let i = 0; i < markers.length; i++) {
        let marker = markers[i];
        let lat = parseFloat(marker.getAttribute('data-lat'));
        let lon = parseFloat(marker.getAttribute('data-lon'));
        let is_selected = marker.getAttribute('data-selected') === 'true';

        if (is_selected) && lat == 12.9086641 {
            marker.style.opacity = '1';
            marker.setAttribute('src', match.image);
            marker.title = match.name;
        } else {
            marker.style.opacity = '0.3';
        }
    }
});

// Reset all
document.getElementById('all-Pro').addEventListener('click', function() {
    location.reload();
});
</script>
"""))

# Save map
m.save("index.html")
