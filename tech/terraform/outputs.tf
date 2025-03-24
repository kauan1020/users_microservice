output "rds_endpoint" {
  value = aws_db_instance.tech_challenge_db.endpoint
}

output "rds_username" {
  value = aws_db_instance.tech_challenge_db.username
}

output "rds_security_group" {
  value = aws_security_group.rds_sg.id
}
