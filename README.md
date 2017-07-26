PSO2 Patchlists
===============

Management file: `http://patch01.pso2gs.net/patch_prod/patches/management_beta.txt`

cUrl: `curl --User-Agent AQUA_HTTP http://patch01.pso2gs.net/patch_prod/patches/management_beta.txt`

	IsInMaintenance=0
	IsExpired=0
	IsLeavePrecede=1
	IsThread=0
	ThreadNum=1
	TimeOut=30000
	ParallelFileSize=10485760
	ParallelThreadNum=1
	CrcThreadNum=1
	FileCacheSize=10485760
	RetryNum=10
	IsPGO=1
	MasterURL=http://download.pso2.jp/patch_prod/v41000_rc_85_masterbase/patches/
	PatchURL=http://download.pso2.jp/patch_prod/v50001_rc_28_583F1C31/patches/

The important list is `PatchURL`, located in: `http://download.pso2.jp/patch_prod/v50001_rc_28_583F1C31/patches/patchlist.txt`

Patchlist format
================

	pso2.exe.pat	13AAAA5783BD0A5F9EFAF2E953CCFA33	29510176	p	g
	PSO2JP.ini.pat	A46C50855C94D122D238F220EFBC1B10	1345	p	g
	sdkencryptedappticket.dll.pat	97FBBC9CAB370638B14FB05A015B2274	526120	p	g
	sdkencryptedappticket64.dll.pat	97243C55A06660CDEC06E87B990C97D5	873768	p	g
	data/win32/7f2368d207e104e8ed6086959b742c75.pat	0D64AC29DFF6F51F90EFA01C2C220BD0	1168704	m	g
	data/win32/da2b663844e3cac930b9333565bf61fe.pat	59B5BF773BBC9B3BA9BF521F65E93DAE	489520	m	g
	data/win32/49cb284c7363c9ee5ab33137afc198b6.pat	878414D949B238C47A7FBF40D758FE36	528812	m	g
	data/win32/6d0c875fb777d4e036e63ef033db716a.pat	2F5F99C2C496D6FC2D265D7A4062D818	632460	m	g

Format is:

	<path> <md5 hash> <size bytes> <master|patch> <uknown flag>

The MasterBase is defined by `MasterUrl` and it seems USELESS. The `PatchURL` seems to contain everything needed.