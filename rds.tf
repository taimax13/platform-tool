# RDS Postgres Instance
module "rds_postgres" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.5.0"
  identifier         = "telemetrydb"
  family = "postgres12"
  engine             = "postgres"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20
  username           = "admin"
  password           = "password"
  skip_final_snapshot = true
  publicly_accessible = false

  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  subnet_ids = module.vpc.private_subnets
}

# Optional: DocumentDB Cluster instead of RDS
# module "docdb_cluster" {
#   source  = "terraform-aws-modules/rds/aws"
#   version = "6.5.0"
#
#   identifier          = "telemetry-cluster"
#   engine              = "docdb"
#   instance_class      = "db.r5.large"
#   master_username     = "admin"
#   master_password     = "password"
#   skip_final_snapshot = true
#   publicly_accessible = false
#
#   vpc_security_group_ids = [aws_security_group.docdb_sg.id]
#
#   subnet_ids = module.vpc.private_subnets
# }