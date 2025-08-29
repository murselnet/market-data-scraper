from mangum import Mangum
from main import app

# Lambda handler with better configuration
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    # Debug bilgisi (geliştirme aşamasında)
    print("Event:", event)
    print("Context:", context)
    
    try:
        response = handler(event, context)
        print("Response:", response)
        return response
    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": f"Internal server error: {str(e)}"
        }




