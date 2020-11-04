# free tier eligible AMI
data "aws_ami" "ami" {
  most_recent = true
  owners = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

resource "aws_instance" "discord_bot" {
  ami           = data.aws_ami.ami.id
  instance_type = "t2.micro"
  user_data = <<EOF
#!/usr/bin/bash
sudo apt-get update -y
sudo apt-get install python3-pip -y
git clone https://github.com/phvv-me/lincoln.git
export DISCORD_TOKEN=${var.DISCORD_TOKEN}
python3 -m pip install -r lincoln/requirements.txt
python3 lincoln/bot/main.py
EOF

  tags = merge(var.tags, {
    name = "${var.tags.project}-ec2-instance"
  })

}

variable "DISCORD_TOKEN" {}