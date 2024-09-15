import grpc
from concurrent import futures
import cache_pb2
import cache_pb2_grpc
import redis
import subprocess

class DNSCacheService(cache_pb2_grpc.CacheServiceStub):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

    def ResolveDomain(self, request, context):
        domain = request.domain
        cached_ip = self.redis_client.get(domain)

        if cached_ip:
            return cache_pb2.DomainResponse(ip_address=cached_ip.decode('utf-8'), cache_hit=True)

        # If not in cache, use `dig` to resolve the domain
        try:
            result = subprocess.run(['dig', '+short', domain], capture_output=True, text=True, check=True)
            ip_address = result.stdout.strip()
            if ip_address:
                self.redis_client.set(domain, ip_address)
                return cache_pb2.DomainResponse(ip_address=ip_address, cache_hit=False)
        except subprocess.CalledProcessError as e:
            context.set_details(f'Error resolving domain: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return cache_pb2.DomainResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_pb2_grpc.add_CacheServiceServicer_to_server(DNSCacheService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('gRPC server running on port 50051')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
