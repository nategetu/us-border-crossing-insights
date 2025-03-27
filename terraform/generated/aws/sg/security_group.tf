resource "aws_security_group" "tfer--default_sg-002D-0a733a58ee3c169df" {
  description = "default VPC security group"

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = "0"
    protocol    = "-1"
    self        = "false"
    to_port     = "0"
  }

  ingress {
    from_port = "0"
    protocol  = "-1"
    self      = "true"
    to_port   = "0"
  }

  name   = "default"
  vpc_id = "vpc-0f54f6770a7592190"
}

resource "aws_security_group" "tfer--launch-002D-wizard-002D-1_sg-002D-09a08ffc019a4da0f" {
  description = "launch-wizard-1 created 2025-03-25T23:49:43.146Z"

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = "0"
    protocol    = "-1"
    self        = "false"
    to_port     = "0"
  }

  ingress {
    cidr_blocks = ["108.28.179.28/32"]
    from_port   = "22"
    protocol    = "tcp"
    self        = "false"
    to_port     = "22"
  }

  name   = "launch-wizard-1"
  vpc_id = "vpc-0f54f6770a7592190"
}
