# Project Structure

* `backend/`: For the FastAPI application.
* `frontend/`: For the Streamlit application.
* `uploads/`: To store uploaded receipts.

# Libraries

* **Backend:**
    * `fastapi`
    * `uvicorn`
    * `SQLAlchemy`
    * `pydantic`
    * `python-multipart`
    * `pytesseract`
    * `python-magic`
* **Frontend:**
    * `streamlit`
    * `requests`
    * `pandas`
    * `plotly`

# Commands

* **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
* **Run backend server:**
  ```bash
  uvicorn backend.main:app --reload --port 8001
  ```
* **Run frontend application:**
  ```bash
  streamlit run frontend/app.py
  ```
