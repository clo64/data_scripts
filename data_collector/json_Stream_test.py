import jsonstreams

with jsonstreams.Stream(jsonstreams.Type.object, filename='foo') as s:
    s.write('foo', 'bar')

s2 = jsonstreams.Stream(jsonstreams.Type.object, filename='Hi')
s2.write('too', ['threw'])
s2.write('welcome', ['hell'])
s2.close()