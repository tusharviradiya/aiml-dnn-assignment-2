"""Fail before assessed training if CUDA or recurrent kernels cannot execute."""
import json,torch
assert torch.cuda.is_available(), 'CUDA is not available in this environment'
name=torch.cuda.get_device_name(0)
assert '1650' in name, name
x=torch.randn(32,128,9,device='cuda',requires_grad=True)
for cls in (torch.nn.RNN,torch.nn.LSTM,torch.nn.GRU):
 model=cls(9,64,batch_first=True).cuda()
 y,_=model(x);loss=y.square().mean();loss.backward()
 assert torch.isfinite(loss) and torch.isfinite(x.grad).all()
 x.grad=None
 torch.cuda.synchronize()
print(json.dumps({'passed':True,'gpu':name,'torch':str(torch.__version__),'cuda':torch.version.cuda,'capability':torch.cuda.get_device_capability(0),'architectures':torch.cuda.get_arch_list()},indent=2))
