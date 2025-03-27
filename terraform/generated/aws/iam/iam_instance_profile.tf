resource "aws_iam_instance_profile" "tfer--S3DynamoDBFullAccessRole" {
  name = "S3DynamoDBFullAccessRole"
  path = "/"
  role = "S3DynamoDBFullAccessRole"
}
