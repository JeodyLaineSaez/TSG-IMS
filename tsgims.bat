@echo off
echo Starting Django Setup...

REM Step 1: You are already in the tsg_ims folder, no need to cd

REM Step 2: Activate virtual environment
call venv\Scripts\activate

REM Step 3: Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Step 4: Run migrations
echo Applying database migrations...
python manage.py migrate

REM Step 5: Start the Django development server in a new terminal window
start "" cmd /k "python manage.py runserver"

REM Step 6: Open web browser to localhost
start http://127.0.0.1:8000

echo Done!

