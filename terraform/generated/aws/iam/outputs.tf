output "aws_iam_instance_profile_tfer--S3DynamoDBFullAccessRole_id" {
  value = "${aws_iam_instance_profile.tfer--S3DynamoDBFullAccessRole.id}"
}

output "aws_iam_role_policy_attachment_tfer--AWSServiceRoleForRedshift_AmazonRedshiftServiceLinkedRolePolicy_id" {
  value = "${aws_iam_role_policy_attachment.tfer--AWSServiceRoleForRedshift_AmazonRedshiftServiceLinkedRolePolicy.id}"
}

output "aws_iam_role_policy_attachment_tfer--AWSServiceRoleForSupport_AWSSupportServiceRolePolicy_id" {
  value = "${aws_iam_role_policy_attachment.tfer--AWSServiceRoleForSupport_AWSSupportServiceRolePolicy.id}"
}

output "aws_iam_role_policy_attachment_tfer--AWSServiceRoleForTrustedAdvisor_AWSTrustedAdvisorServiceRolePolicy_id" {
  value = "${aws_iam_role_policy_attachment.tfer--AWSServiceRoleForTrustedAdvisor_AWSTrustedAdvisorServiceRolePolicy.id}"
}

output "aws_iam_role_policy_attachment_tfer--S3DynamoDBFullAccessRole_AmazonDynamoDBFullAccess_id" {
  value = "${aws_iam_role_policy_attachment.tfer--S3DynamoDBFullAccessRole_AmazonDynamoDBFullAccess.id}"
}

output "aws_iam_role_policy_attachment_tfer--S3DynamoDBFullAccessRole_AmazonS3FullAccess_id" {
  value = "${aws_iam_role_policy_attachment.tfer--S3DynamoDBFullAccessRole_AmazonS3FullAccess.id}"
}

output "aws_iam_role_tfer--AWSServiceRoleForRedshift_id" {
  value = "${aws_iam_role.tfer--AWSServiceRoleForRedshift.id}"
}

output "aws_iam_role_tfer--AWSServiceRoleForSupport_id" {
  value = "${aws_iam_role.tfer--AWSServiceRoleForSupport.id}"
}

output "aws_iam_role_tfer--AWSServiceRoleForTrustedAdvisor_id" {
  value = "${aws_iam_role.tfer--AWSServiceRoleForTrustedAdvisor.id}"
}

output "aws_iam_role_tfer--S3DynamoDBFullAccessRole_id" {
  value = "${aws_iam_role.tfer--S3DynamoDBFullAccessRole.id}"
}

output "aws_iam_user_policy_attachment_tfer--Admin_AdministratorAccess_id" {
  value = "${aws_iam_user_policy_attachment.tfer--Admin_AdministratorAccess.id}"
}

output "aws_iam_user_tfer--AIDAT24SXHO5QKNKDXA36_id" {
  value = "${aws_iam_user.tfer--AIDAT24SXHO5QKNKDXA36.id}"
}
