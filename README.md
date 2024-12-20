# Real-Time Chat System with SSE

This project implements a real-time chat system using **FastAPI** and **Server-Sent Events (SSE)**. The system allows users to send messages, retrieve messages within a specific time range, and stream real-time updates for new messages.

----------

## Features

1.  **Send Messages**:
    
    -   Users can send messages to the system via a REST API endpoint.
        
    -   Each message includes the sender's username, the content, and a timestamp.
        
2.  **Retrieve Messages**:
    
    -   Retrieve messages within a specified time range using query parameters (`start_date` and `end_date`).
        
    -   Date format: `YYYY-MM-DD HH:MM:SS`.
        
3.  **Real-Time Streaming**:
    
    -   Stream new messages in real-time using Server-Sent Events (SSE).
        
    -   Clients can subscribe to the `/stream` endpoint to receive live updates as new messages are added.
        
4.  **Modular Design**:
    
    -   Code is organized into services and modules for better maintainability and scalability.
        

----------

## Requirements

-   **Python 3.8+**
    
-   **FastAPI**
    
-   **uvicorn**

## Installation

```python
pip install -r requirements.txt
```

1.  **Start the Server**:
    
    ```
    uvicorn app.main:app --reload
    ```
    
2.  **Access the API Documentation**:
    
    -   Open your browser and navigate to:
        
        -   Swagger UI: http://127.0.0.1:8000/docs
## Future Improvements

1.  Add user authentication for secure message handling.
    
2.  Implement persistent storage (e.g., SQLite, PostgreSQL) for messages.
    
3.  Enhance the SSE logic to include reconnection handling for clients.
    
4.  Add pagination and sorting for message retrieval.
