module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  cluster_name    = "${var.project_name}-${var.environment}-cluster"
  cluster_version = "1.27"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  eks_managed_node_group_defaults = {
    #ami_type       = "AL2_x86_64"
    instance_types = var.instance_types
  }
  eks_managed_node_groups = {
    initial = {
      min_size     = 1
      max_size     = 3
      desired_size = 2
      instance_types = var.instance_types
      capacity_type  = "ON_DEMAND"
    }
  }

  enable_irsa = true

  tags = {
    Environment = var.environment
    Product     = var.project_name
  }
}