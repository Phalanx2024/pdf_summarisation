import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda function handler.

    Args:
        event: The event dict containing request data
        context: Lambda context object with runtime info

    Returns:
        API Gateway compatible response dict
    """
    logger.info(f"Received event: {json.dumps(event)}")

    body = event.get("body")
    query_params = event.get("queryStringParameters") or {}

    # Parse JSON body if present
    if body and isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Invalid JSON body"})
            }

    # Example business logic
    name = query_params.get("name") or (body.get("name") if body else None) or "World"

    response_body = {
        "message": f"Hello, {name}!",
        "method": http_method,
        "requestId": context.aws_request_id if context else "local"
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response_body)
    }


# For local testing
if __name__ == "__main__":
    # Mock context for local testing
    class MockContext:
        aws_request_id = "local-test-123"

    test_event = {
        "httpMethod": "GET",
        "queryStringParameters": {"name": "Developer"}
    }

    result = lambda_handler(test_event, MockContext())
    print(json.dumps(result, indent=2))
