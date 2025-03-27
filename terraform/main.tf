terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  shared_config_files      = ["~/.aws/config"]
  shared_credentials_files = ["~/.aws/credentials"]
  region                   = "us-east-1"
}

# Create AWS resources

resource "aws_security_group" "ec2_security_group" {
  name = "ec2_security_group"
  
}

resource "aws_s3_bucket" "border_crossings_bucket" {
  bucket = "border-crossing-bucket"

  tags = {
    Name = "border-crossing-bucket"
  }
}

# i should switch this to athena
resource "aws_redshift_cluster" "border_crossings_redshift" {
  cluster_identifier = "bcb-redshift-cluster"
  database_name      = "bcbdb"
  master_username    = "zoomcamp"
  master_password    = "Z0omcamp"
  node_type          = "dc2.large"
  cluster_type       = "single-node"
}

# ec2 cluster