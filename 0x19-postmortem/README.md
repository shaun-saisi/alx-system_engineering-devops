Postmortem Report
Incident Summary: Upon the release of ALX's System Engineering & DevOps project 0x19, an outage occurred on an isolated Ubuntu 14.04 container running an Apache web server at approximately 06:00 East African Time (EAT) here in Kenya. The server returned 500 Internal Server Errors for GET requests instead of the expected HTML file for a simple Holberton WordPress site.
Debugging Process: The issue was first identified by Brennan (BDB), who initiated the debugging process around 19:20 EAT.
Initial Checks:
Verified running processes using ps aux. Observed two apache2 processes: one owned by root and the other by www-data.
Configuration Inspection:
Checked the /etc/apache2/sites-available directory. Confirmed that the server was serving content from /var/www/html/.
Strace Analysis on Root Process:
Ran strace on the PID of the root Apache process while sending a curl request to the server. The output provided no useful information.
Strace Analysis on www-data Process:
Repeated the strace on the www-data process with lowered expectations. This time, strace revealed an -1 ENOENT (No such file or directory) error when attempting to access /var/www/html/wp-includes/class-wp-locale.phpp.
Error Identification:
Inspected files in the /var/www/html/ directory using Vim pattern matching. Located the erroneous .phpp file extension in wp-settings.php (Line 137: require_once( ABSPATH . WPINC . '/class-wp-locale.php' );).
Error Correction:
Removed the trailing p from the line.
Verification:
Tested the server again using curl, which returned a 200 OK response.
Automation:
Created a Puppet manifest to automate the correction of similar errors in the future.
Summation: The issue was due to a typo in the wp-settings.php file where class-wp-locale.phpp was mistakenly written instead of class-wp-locale.php. Correcting this typo resolved the outage.
Prevention: To prevent such incidents in the future:
Testing:
Thoroughly test the application before deployment to catch errors early.
Status Monitoring:
Implement uptime-monitoring services like UptimeRobot to receive immediate alerts upon website outages.
Automation: A Puppet manifest (0-strace_is_your_friend.pp) was written to replace any .phpp extensions with .php in wp-settings.php to automate fixing similar errors.


