Vagrant.configure("2") do |config|
  config.vm.provider "docker" do |d|
    d.image = "python:3.7-alpine"
    d.has_ssh = true
    d.remains_running = true
    # d.compose = true
  end
  config.vm.provision "shell", inline: <<-SHELL
    python -m pip install pipenv
    pipenv install --system --deploy --ignore-pipfile
    apk update
    apk add build-base postgresql postgresql-dev postgresql-server libpq unzip
    postgresql-setup initdb
    systemctl enable postgresql
    systemctl start postgresql
    postgres -c 'createuser -dRS vagrant'
    su vagrant -c 'createdb news'
    unzip db/data/newsdata.zip
    psql -d news -f db/data/newsdata.sql
  SHELL
end
