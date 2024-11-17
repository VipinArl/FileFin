# FileFin
A file rename utility for Jellyfin media server.

## How To:
 1. Get the repository locally, setup your virtual environment, and install dependencies. (minimum step - execute `pip install -r requirements.txt`)
 2. Get your API key from 'https://www.themoviedb.org/settings/api' and add it in the `setup.py` file.
 3. Execute `python main.py` - This will open the application window.
 4. Select the directory which has your media files - This will list all the files recursively.
 5. Select _Predict Names_ to get the Jellyfin expected file name, which is _movie name (year)_.
 6. If a movie is predicted properly, the row will be marked as GREEN.
 7. If there are multiple predictions, the row color will be YELLOW. You can double click the row (Or right click and select _Choose Prediction_), select the proper name, and the row will be marked as GREEN.
 8. If there is no proper result, the row will be marked as RED. You have multiple options here
    i. Double click and manually enter the name. The row will be marked as GREEN.
    ii. Select _Edit Pattrens_ and add undesired patterns present in the file name and save the patterns. Then right click and select _Predict_, which will predict the name if there are no more extra words in the name. Once the name is predicted properly, the row will be marked as GREEN.
 9. If you want to stop the predictions at any point you can click the red cancel button. You can fix the names which are predicted so far in this case.
 10. Once you are satified with all the names, click _Fix Names_ and all the predicted files will be renamed after confirmation.
 11. Please note: *Rename will happen **even if the row is not GREEN**.*
 12. Enjoy your weekends!

## Feature request
1. If you need a new feature, just ask.
2. If you find a bug, just kill! (kidding, tell me please. will fix it)

### Just for testing
Testing always gives confidence. The file `test.py` can be used to create a replica of your movie directory with dummy files. You can execute FileFin and check whether it works for you before you rename the actual files. Yes, I did this!
