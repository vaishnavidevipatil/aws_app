import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Product')

def lambda_handler(event, context):

    if(event['operation'] == 'addProduct'):
        return saveProduct(event) 
    else: 
        return getProducts()
    
def saveProduct(event):
    # Normalize keys
    product_code = event.get('productCode') or event.get('productcode')
    price = event.get('price')

    if not product_code:
        return {
            'statusCode': 400,
            'body': json.dumps("Error: 'productCode' key is missing from the event.")
        }

    if not price:
        return {
            'statusCode': 400,
            'body': json.dumps("Error: 'price' key is missing from the event.")
        }

    gmt_time = time.gmtime()
    now = time.strftime('%a, %d %b %Y %H:%M:%S', gmt_time)

    table.put_item(
        Item={
            'productCode': product_code,
            'price': price,
            'createdAt': now
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Product with ProductCode: ' + product_code + ' created at ' + now)
    }

def getProducts():

    response = table.scan()
    
    items = response['Items']
    print(items)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(items),
        'headers': {
            'Content-Type': 'application/json',
        }
    } 