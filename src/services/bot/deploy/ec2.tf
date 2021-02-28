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
  ami           = "ami-03d315ad33b9d49c4"
  instance_type = "t2.micro"
  user_data = <<EOF
#!/usr/bin/bash
sudo apt-get update -y
sudo apt-get install python3-pip -y

git clone https://github.com/phvv-me/lincoln.git

export DISCORD_TOKEN=${var.DISCORD_TOKEN}
export AWS_ACCESS_KEY_ID=${var.AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${var.AWS_SECRET_ACCESS_KEY}
export AWS_DEFAULT_REGION=us-east-1

cd lincoln/src/services/

python3 -m pip install -r bot/requirements.txt
python3 run_bot.py
EOF

  tags = merge(var.tags, {
    name = "bot-ec2-instance"
  })
}
