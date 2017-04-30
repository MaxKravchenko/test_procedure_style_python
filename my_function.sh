checkFile()
{
	if  [ -f $1 ]; then  
		echo "The File '$1' Exist. Next step..."
	else
		echo "The File '$1' Does Not Exist. Program stopped."
		exit 0 
	fi
}	