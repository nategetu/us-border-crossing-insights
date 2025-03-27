resource "aws_iam_user_policy_attachment" "tfer--Admin_AdministratorAccess" {
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
  user       = "Admin"
}
