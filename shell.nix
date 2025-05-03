with import <nixpkgs> {};

mkShell {
	buildInputs = [
		python312
		python312Packages.virtualenv
		python312Packages.mysqlclient
		git
		mariadb
		nodejs
	];
	shellHook = ''
		if [ ! -d .venv ]; then
			python -m venv .venv
		fi
		source .venv/bin/activate

		# JS deps (only runs once per clone)
		if [ ! -d frontend/node_modules ]; then
			npm install
		fi
	'';


}
