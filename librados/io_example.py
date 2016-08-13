import rados

try:
        cluster = rados.Rados(conffile='')
except TypeError as e:
        print 'Argument validation error: ', e
        raise e

print "Created cluster handle."

try:
        cluster.connect()
except Exception as e:
        print "connection error: ", e
        raise e
finally:
        print "Connected to the cluster."

print "\n\nI/O Context and Object Operations"
print "================================="

cluster_stats = cluster.get_cluster_stats()
print cluster_stats

print "\nCreate 'data8' Pool"
print "------------------"
cluster.create_pool('data8')
pools = cluster.list_pools()
for pool in pools:
	print pool


ioctx = cluster.open_ioctx('data8')
print "\nWriting object 'hw' with contents 'Hello World!' to pool 'data'."
ioctx.write("hw", "Hello World!")

print "\nContents of object 'hw'\n------------------------"
print ioctx.read("hw")

print "\nClosing the connection."
ioctx.close()

print "Shutting down the handle."
cluster.shutdown()





