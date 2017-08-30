# Disiem

Diversity analysis of the dataset with the following software:
  
  - Suricata
  - Bro
  - Palo Alto Firewall
  - Mcafee
  - Cisco VPN
  - Cisco Firewall
  
A single request json object from alert logs:

 `{"dstPostNAT":"0.0.0.0","srcPort":"57122","Flags":"0x19","server_name":"sinfwo302a","dst":"10.23.70.11","sourceType":"pan_firewall","VirtualSystem":"vsys1","RepeatCount":"1","totalBytes":"506","dstPostNATPort":"0","datetime":"2017-04-15T00:00:00+00:00","LogForwardingProfile":"log-all-to-panorama-and-ext","dstBytes":"251","proto":"udp","EgressInterface":"ae1.420","ElapsedTime":"0","SourceZone":"vgw","RuleName":"GWAN to UFIS","totalPackets":"2","srcPostNATPort":"0","srcBytes":"255","Application":"ldap","IngressInterface":"ae1.501","src":"10.30.1.100","dstPort":"389","srcPostNAT":"0.0.0.0","URLCategory":"any","DestinationZone":"office","cat":"TRAFFIC","SessionID":"28853","action":"allow","Subtype":"end","SerialNumber":"001801029476","Type":"TRAFFIC"}`

## Storage

Split data into overlapping timeslices and load two minute sections from each device / software combination. A register is kept for each increment of delta time, marking the file and position to continue in 2 steps. Timeslices begin at 1/2 of the previous slice to catch overlapping network sessions between the log increments. Every alert/request is loaded twice and checked with the previous and following time slice.

![siganalyzer_segments](https://user-images.githubusercontent.com/6486510/29896111-a3080aaa-8dd3-11e7-920c-493a0599b2ce.png)

## Wrapper

Each software's log can contain different field names and datetime formats which require custom dictionary subclasses to abstract the interaction with the varying json structures.
