provider "aws" {
  region  = "us-east-1"
  profile = "terraform-test"
}


resource "aws_db_instance" "tech_challenge_db" {
  identifier             = "tech-challenge-db"
  allocated_storage      = 20
  storage_type          = "gp2"
  engine                = "postgres"
  engine_version        = "12.21"
  instance_class        = "db.t3.micro"
  username              = "app_user"
  password              = "app_password"
  parameter_group_name  = "default.postgres12"
  publicly_accessible   = true
  skip_final_snapshot   = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  tags = {
    Name = "TechChallengeDB"
  }
}

resource "aws_security_group" "rds_sg" {
  name_prefix = "rds-security-group"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
