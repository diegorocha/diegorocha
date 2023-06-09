terraform {
  required_version = "1.4.5"
  required_providers { aws = { version = "5.1.0" } }
  backend "s3" {
    bucket               = "diegor-terraform"
    workspace_key_prefix = ""
    key                  = "diegorocha.com.br/terraform.tfstate"
    region               = "us-east-1"
    profile              = "diego"
  }
}
