import plotly.express as px
px.set_mapbox_access_token(
    "pk.eyJ1IjoieHlsZWNpb24iLCJhIjoiY2s2azJtaGV2MDJnNTNra3kxYmZ3YTlzdiJ9.s_EicZR1hfYNpWxZJfLMSQ")
df = px.data.carshare()
fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
fig.show()
