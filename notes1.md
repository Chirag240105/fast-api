# FastAPI Notes for Docker + Machine Learning

## 1. What is FastAPI?

FastAPI is a modern, high-performance Python web framework used to build APIs.

It is commonly used for:
- Backend development
- REST APIs
- Machine Learning model deployment
- Deep Learning inference APIs
- Microservices

FastAPI is built on two important libraries:

- **Starlette:** Handles web requests, routing, middleware, and asynchronous web functionality.
- **Pydantic:** Validates request data and converts it into the expected Python types.

**Uvicorn** is an ASGI server commonly used to run FastAPI applications.

---

## 2. Advantages of FastAPI

1. High performance
2. Automatic request-data validation
3. Automatic API documentation
4. Supports asynchronous programming
5. Easy integration with ML and DL models
6. Type hints improve code readability
7. Supports dependency injection
8. Suitable for microservices and backend applications

Automatic API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Why Is FastAPI Fast?

### A. Asynchronous Programming

FastAPI supports `async` and `await`, which are useful for I/O-bound operations such as:
- Database queries
- External API calls
- Network requests
- Reading data from services

Example:

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def home():
    await asyncio.sleep(1)
    return {"message": "Hello World"}
```

While one request waits for an I/O operation, the server can work on other requests.

**Important:** `async` does not automatically make CPU-intensive tasks or ML model inference faster.

### B. ASGI Support

ASGI stands for **Asynchronous Server Gateway Interface**.

It allows an application server to communicate with an asynchronous Python web application.

FastAPI uses ASGI, which supports asynchronous request handling and WebSockets.

### C. Pydantic Validation

Pydantic validates incoming data using Python type annotations.

Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

If an API expects an integer for `age`, invalid input can be rejected automatically.

### D. Uvicorn

Uvicorn is an ASGI server used to run FastAPI applications.

Install and run:

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Here:
- `main` is the Python file name, without `.py`.
- `app` is the FastAPI application variable.
- `--reload` restarts the server when code changes. It is mainly for development.

---

## 4. WSGI vs ASGI

### WSGI

WSGI stands for **Web Server Gateway Interface**.

It is the traditional interface between Python web applications and web servers.

Commonly associated with traditional synchronous applications, including many Flask deployments.

### ASGI

ASGI stands for **Asynchronous Server Gateway Interface**.

It supports asynchronous applications and features such as WebSockets.

FastAPI is an ASGI framework.

| Feature | WSGI | ASGI |
|---|---|---|
| Main use | Traditional Python web apps | Modern asynchronous web apps |
| Async support | Not native to the interface | Supported |
| WebSockets | Not directly supported by WSGI itself | Supported |
| Example | Traditional Flask deployment | FastAPI with Uvicorn |

**Remember:** WSGI is an interface specification, not a web server itself.

---

## 5. Flask vs FastAPI

| Feature | Flask | FastAPI |
|---|---|---|
| Type | Lightweight web framework | Modern API framework |
| Data validation | Often requires additional tools | Built-in through Pydantic |
| Type hints | Supported | Central to validation and API definitions |
| API documentation | Usually requires extensions | Automatically generated |
| Async support | Available with limitations | Designed for ASGI and async |
| ML deployment | Supported | Very suitable |
| Learning curve | Simple | Simple, with additional typing concepts |

**Interview answer:**

FastAPI is often a good choice for APIs that need request validation, automatic documentation, and asynchronous I/O. Flask is also useful for lightweight applications. Actual performance depends on the workload, libraries, server configuration, and implementation.

---

## 6. Path Parameters

A path parameter is a value included directly in the URL.

Example URL:

```text
http://127.0.0.1:8000/users/10
```

Code:

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., gt=0)):
    return {"user_id": user_id}
```

Explanation:
- `user_id` comes from the URL.
- `int` specifies the expected data type.
- `Path(...)` marks the parameter as required and allows validation constraints.
- `gt=0` means the value must be greater than zero.

Example:

```text
/users/10   -> Valid
/users/0    -> Validation error
/users/abc  -> Validation error
```

---

## 7. Query Parameters

Query parameters are values supplied after `?` in a URL.

Example:

```text
http://127.0.0.1:8000/products?category=mobile&limit=5
```

Code:

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/products")
def get_products(
    category: str | None = None,
    limit: int = Query(default=10, ge=1, le=100)
):
    return {
        "category": category,
        "limit": limit
    }
```

Explanation:
- `category` is optional because its default is `None`.
- `limit` defaults to `10`.
- `ge=1` means greater than or equal to one.
- `le=100` means less than or equal to 100.

Example:

```text
/products
/products?category=mobile
/products?category=mobile&limit=5
```

### Path vs Query Parameters

| Path Parameter | Query Parameter |
|---|---|
| Identifies a resource | Filters or modifies a request |
| `/users/10` | `/users?age=20` |
| Defined inside `{}` in the route | Usually appears after `?` |

---

## 8. Common Validation Constraints

| Constraint | Meaning |
|---|---|
| `gt=0` | Greater than zero |
| `ge=0` | Greater than or equal to zero |
| `lt=100` | Less than 100 |
| `le=100` | Less than or equal to 100 |
| `min_length=3` | Minimum string length of 3 |
| `max_length=50` | Maximum string length of 50 |

These constraints can be used with tools such as `Path`, `Query`, and Pydantic's `Field`, depending on the parameter or model field being validated.

---

## 9. FastAPI for Machine Learning

FastAPI can expose an ML model through an HTTP API.

Typical workflow:

1. Train the model using scikit-learn, PyTorch, or TensorFlow.
2. Save the trained model.
3. Load the model when the API application starts.
4. Accept input data through an endpoint.
5. Validate the input.
6. Run model inference.
7. Return the prediction as JSON.

Example using a saved scikit-learn model:

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# Load the trained model once when the application starts.
model = joblib.load("model.joblib")


class PredictionInput(BaseModel):
    feature_1: float
    feature_2: float


@app.post("/predict")
def predict(data: PredictionInput):
    features = [[data.feature_1, data.feature_2]]

    prediction = model.predict(features)

    return {
        "prediction": prediction.tolist()
    }
```

**Important:** The input features and their order must match the features used to train the model. The example assumes the saved model expects exactly two numeric features.

Do not reload the model for every request unless there is a specific reason to do so.

---

## 10. What Is Docker?

Docker is a platform used to package an application and its dependencies into a container image.

A container helps the application run more consistently across different environments.

### Why use Docker with FastAPI and ML?

- Packages Python dependencies.
- Makes application deployment more consistent.
- Helps standardize development and production environments.
- Can package model files when appropriate.
- Simplifies running the same service on different machines.

### Common Docker Terms

| Term | Meaning |
|---|---|
| Dockerfile | Instructions to build an image |
| Image | Packaged application template |
| Container | Running instance of an image |
| Port mapping | Connects a host port to a container port |
| Volume | Provides persistent or shared storage |

### Example Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Example requirements.txt

```text
fastapi
uvicorn[standard]
pydantic
joblib
scikit-learn
```

Use compatible package versions for your project, and pin versions for reproducible deployments.

### Build and Run

Build the image:

```bash
docker build -t fastapi-ml-app .
```

Run the container:

```bash
docker run -p 8000:8000 fastapi-ml-app
```

Open:

```text
http://127.0.0.1:8000/docs
```

The `-p 8000:8000` argument maps port 8000 on your computer to port 8000 inside the container.

**Production note:** For large ML models, consider model storage, startup time, memory usage, inference latency, and whether the model should be downloaded or mounted at runtime.

---

## 11. Quick Revision

- **FastAPI:** Python framework for building APIs.
- **Starlette:** Web functionality and request handling.
- **Pydantic:** Data validation and parsing.
- **Uvicorn:** ASGI server that runs the application.
- **ASGI:** Interface supporting asynchronous applications.
- **WSGI:** Traditional Python web application interface.
- **Path parameter:** Value embedded in a URL path.
- **Query parameter:** Value supplied after `?` in a URL.
- **Docker:** Packages applications and dependencies into containers.
- **ML inference:** Using a trained model to generate predictions.
- **`async` / `await`:** Syntax for asynchronous operations.
- **`/docs`:** Automatically generated interactive API documentation.

---

## 12. Interview Questions

### Q1. Why is FastAPI considered fast?

It uses Starlette, supports ASGI and asynchronous I/O, and uses Pydantic for validation. Actual performance depends on the workload and implementation.

### Q2. What is the difference between ASGI and WSGI?

WSGI is a traditional interface for Python web applications. ASGI supports asynchronous application patterns and WebSockets.

### Q3. What is the role of Uvicorn?

Uvicorn is an ASGI server that runs an application such as FastAPI.

### Q4. Why is Pydantic used?

Pydantic validates and parses data based on declared types and constraints.

### Q5. How do you deploy an ML model with FastAPI?

Load the trained model, create an endpoint, validate input, run inference, and return the prediction in a JSON response.

### Q6. Why use Docker?

Docker packages the application and dependencies into a portable container image, making deployment more consistent.

### Q7. Does async make ML inference faster?

Not necessarily. Async is especially useful for I/O-bound work. CPU- or GPU-intensive inference may require separate workers, batching, concurrency controls, or dedicated model-serving infrastructure.

### Q8. What is the difference between a path parameter and a query parameter?

A path parameter identifies a resource, such as `/users/10`. A query parameter filters or configures a request, such as `/users?limit=10`.
