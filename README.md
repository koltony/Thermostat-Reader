# Thermostat-Reader
This algorythm can recognize seven segment displays on a thermostat. 

All the settings are in the JSON file.
This algorytm isnt plug-and-play you have to add the screen's aspect ratio and the recognizeing sensitivity:
<img width="324" alt="Screenshot 2022-03-11 at 18 57 43" src="https://user-images.githubusercontent.com/65023553/157923643-f77e4fb7-ad9a-451d-8eef-476af95ab62b.png">

Then you have to set up the regions, you can add as many regions as you want.
A region have to include a name, the maximum amount of digits that region that can display, the format(1 is temperature,2 is time, 3 is program).
<img width="275" alt="Screenshot 2022-03-11 at 19 01 19" src="https://user-images.githubusercontent.com/65023553/157924532-f26472fb-637a-419d-ac36-5f89b9091020.png">
And last you have to scpecify the location, in this case the aspect ratio is 3x4.5 so the screen will be 300x450 pixels

<img width="257" alt="Screenshot 2022-03-11 at 19 13 37" src="https://user-images.githubusercontent.com/65023553/157925855-dd42df05-361d-4678-b632-64b282d919bf.png">

After you finished with the settings you can run the app through main.py
Select an image from the folder where your images are, image names have to be "image" + "1,2...156"
<img width="814" alt="Screenshot 2022-03-11 at 18 50 07" src="https://user-images.githubusercontent.com/65023553/157925972-091d7769-e163-4f4e-9625-3172e475417d.png">

For perspective transform, select the 4 corner of the screen from top-left to top-right to bottom-left to bottom right
<img width="851" alt="Screenshot 2022-03-11 at 18 50 29" src="https://user-images.githubusercontent.com/65023553/157926021-f65b3c47-6c45-437c-9800-b3e126a13573.png">
If you messed it up you can hit r, if its good than hit enter

At the end you can save the excel file with the results
<img width="364" alt="Screenshot 2022-03-11 at 18 49 31" src="https://user-images.githubusercontent.com/65023553/157926441-ae237c97-6f92-4f42-bbcd-55af8fa26a05.png">
<img width="439" alt="Screenshot 2022-03-11 at 19 18 52" src="https://user-images.githubusercontent.com/65023553/157926634-cc7d2027-a050-4d75-938c-4e78d3dd59e3.png">

