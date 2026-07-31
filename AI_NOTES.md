# AI_NOTES.md

## AI Usage

I used both ChatGPT and Claude while building this project.

### What AI helped with

* I used **ChatGPT** to generate the initial project structure and folder organization.
* I used **Claude** to generate most of the FastAPI code, including the models, routes, service layer, and test cases.

### What I changed

* While running the project, I got an import error because the `src/routes/expense_routes.py` file had accidentally become **0 bytes**. The editor was showing the code, but the file saved on disk was empty due to a terminal paste issue. I identified the problem, recreated the file with the correct content, and verified that the routes imported correctly.
* Fixed a few import and routing issues while testing the application.
* Reviewed the generated code and confirmed that validation, API responses, and status codes matched the assignment requirements.
* Updated the README with the correct installation, run, and test commands.

### AI suggestions I didn't use

* I did not use a database because the assignment only required in-memory or JSON file storage.
* I did not add extra features beyond the assignment requirements to keep the project simple and focused.

### How I verified the project

* Started the server using `uvicorn src.main:app --reload`.
* Tested all endpoints through the FastAPI Swagger UI (`/docs`).
* Ran the test suite using `python -m pytest -v`.
* Confirmed that expenses were stored correctly in the JSON file and that all required features worked as expected.
