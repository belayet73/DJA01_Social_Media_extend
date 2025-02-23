
Key Highlights:
✅ core/ contains the main app with models, views, forms, templates, and static files.
✅ static/ holds CSS files and uploaded images (organized into profile_pics/ and posts/).
✅ media/ stores user-uploaded files dynamically.
✅ templates/ contains HTML files for different pages.
✅ settings.py is configured to serve static and media files properly.
✅ db.sqlite3 is the database file (for development).


sample user accounts
-------------------------
user	  | password
-------------------------
testuser1 | password123;
testuser2 | password123;
testuser3 | password123;
testuser4 | password123;


How  to install:
Step 1 : Ensure you have Python (3.8 or later) installed. You can check by running:
python --version

Step 2: Clone the Project Repository
	Navigate to a folder where you want to store the project and clone the repository (if using Git):
	git clone https://github.com/your-username/your-repo.git
	cd your-repo

	(Replace your-username/your-repo with the actual GitHub repository URL.)

	If you don’t have Git, download the ZIP from GitHub and extract it manually.

Step 3: Create and Activate a Virtual Environment
	pipenv shell

Step 4: Install Dependencies
	pip install django pillow 

Step 5: Configure Database

	python manage.py makemigrations
	python manage.py migrate

Step 6: Create a Superuser (Admin Access)
	python manage.py createsuperuser
	Username: admin
	Password: admin

Step 7: Collect Static Files
	python manage.py collectstatic

Step 8: Run the Django Server
	python manage.py runserver

	Open http://127.0.0.1:8000/ in your web browser.

Step 9: Access the Admin Panel
	http://127.0.0.1:8000/admin/
	Login with your superuser credentials (admin/admin).
