PSO2 Patchlists
===============

`PatchBase` will now refer to the `PatchURL` repository, `MasterBase` will now refer to the `MasterURL` repository.  

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
	PatchURL=http://download.pso2.jp/patch_prod/v50000_rc_101_416B9870/patches/

The important list is `PatchURL`, located in: `http://download.pso2.jp/patch_prod/v50001_rc_28_583F1C31/patches/patchlist.txt`  
That list is the one that seems to be used to updated the game since it checks and downloads from the `MasterURL` and `PatchURL`.

The official launcher seems to deny updates and filechecking when `IsInMaintenance` is set to `1`.

Another `management_beta.txt` file exist at `http://download.pso2.jp/patch_prod/patches/management_beta.txt` but it isn't used since the version don't match.


Patchlist format
================

The right list to use is the `PatchBase`'s `patchfile.txt`.

	pso2.exe.pat	13AAAA5783BD0A5F9EFAF2E953CCFA33	29510176	p	g
	PSO2JP.ini.pat	A46C50855C94D122D238F220EFBC1B10	1345	p	g
	sdkencryptedappticket.dll.pat	97FBBC9CAB370638B14FB05A015B2274	526120	p	g
	sdkencryptedappticket64.dll.pat	97243C55A06660CDEC06E87B990C97D5	873768	p	g
	data/win32/7f2368d207e104e8ed6086959b742c75.pat	0D64AC29DFF6F51F90EFA01C2C220BD0	1168704	m	g
	data/win32/da2b663844e3cac930b9333565bf61fe.pat	59B5BF773BBC9B3BA9BF521F65E93DAE	489520	m	g
	data/win32/49cb284c7363c9ee5ab33137afc198b6.pat	878414D949B238C47A7FBF40D758FE36	528812	m	g
	data/win32/6d0c875fb777d4e036e63ef033db716a.pat	2F5F99C2C496D6FC2D265D7A4062D818	632460	m	g

Format is:

	<path> <md5 hash> <size bytes> <master|patch> <unknown flag>

The `unknown flag` might be use for gradual download. As usual remove the `.pat` extension when downloading.

Version files
=============

Using the `PatchBase` we can retrieve the current version of the game in the files `version.ver` and `gameversion.ver.pat`. These files don't seem to exist in the `MasterBase`.

	$> curl --User-Agent AQUA_HTTP http://download.pso2.jp/patch_prod/v50000_rc_101_416B9870/patches/version.ver
	v50000_rc_101
	$> curl --User-Agent AQUA_HTTP http://download.pso2.jp/patch_prod/v50000_rc_101_416B9870/patches/gameversion.ver.pat
	5.0001.2

Ìt seems only `gameversion.ver.pat` is now used.
