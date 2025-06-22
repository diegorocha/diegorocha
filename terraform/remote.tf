data "terraform_remote_state" "infra" {
  backend = "s3"

  config = {
    bucket               = "diegor-terraform"
    workspace_key_prefix = ""
    key                  = "diegor-infra/terraform.tfstate"
    region               = "us-east-1"
  }
}
