# free tier eligible AMI
data "aws_ami" "ami" {
  most_recent = true
  owners = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

resource "aws_security_group" "allow_all_out" {
  name        = "allow all out"
  description = "Allow all outbound traffic"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    name = "${var.tags.project}-sg"
  })
}

resource "aws_instance" "discord_bot" {
  ami           = data.aws_ami.ami.id
  instance_type = "t2.micro"
  security_groups = [aws_security_group.allow_all_out.name]
  user_data_base64 = filebase64("../bot/entrypoint.sh")

  tags = merge(var.tags, {
    name = "${var.tags.project}-ec2-instance"
  })

  provisioner "file" {
    source      = "../.env"
    destination = "lincoln/.env"
  }
}
