# Visualizing Spatial Data
## kehinde obanla
### Description:
#### Points:

- The repo already has the ability to place points onto the map. 
  - Add the ability to save those points to a json file and reload them later.
  - Add a text box that allows you to put a lat/lon in the box, and a submission will find nearest neighbors from any one of our many data sets (earthquakes, ufos, volcanoes, plane crashes) 

#### Lines: 

- The repo has line drawing capability already. Instead of saving the lines to a json file, add the ability to choose a starting and ending point both from separate dropdown menus (like cities). When the second point is chosen, a line will get drawn and a distance calculated between the two chosen points will be displayed in some clear manner.

#### Minimum Area Bounding Box

- Draw a rectangle on the map somewhere. This will query the backend and find all points (again from whatever data file) within the bounding rectangle and display them in some manner. 

#### Minimum Area Polygon

- Draw a polygon around a cluster of points (again, it could be fake data, or any one of the many data files we have) and the polygon will "snap tight" like a rubber band around the points inside the polygon. 

#### GeoJson

- Upload or paste a GeoJson file into a textarea and display it on the map.

#### View Railroads

- Add a flask route to return all railroads within a given US State. 
#### Files
|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |