param(
    [int[]]$Ports = @((3000..3010) + 5173 + (8000..8010)),
    [switch]$KillDevProcesses
)

Write-Host "Freeing ports: $($Ports -join ', ')"

function Stop-PortProcess([int]$Port) {
    try {
        $conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        if ($conns) {
            $procIds = $conns | Select-Object -ExpandProperty OwningProcess -Unique
            foreach ($procId in $procIds) {
                try {
                    $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
                    if ($null -ne $proc) {
                        Write-Host "Killing PID $procId ($($proc.ProcessName)) using port $Port"
                        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
                    } else {
                        Write-Host "Killing PID $procId using port $Port"
                        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
                    }
                } catch {}
            }
        } else {
            Write-Host "No process found using port $Port"
        }
    } catch {
        Write-Host "Failed to inspect port $($Port): $($_)"
    }
}

foreach ($p in $Ports) { Stop-PortProcess -Port $p }

if ($KillDevProcesses) {
    Write-Host "Scanning for common dev processes (uvicorn, node next/vite/react-scripts, npm/yarn/pnpm dev)..."
    try {
        $procs = Get-CimInstance Win32_Process | Where-Object {
            ($_.Name -match 'uvicorn') -or
            (($_.Name -match 'python') -and ($_.CommandLine -match 'uvicorn')) -or
            (($_.Name -match 'node') -and ($_.CommandLine -match '(next|vite|react-scripts|webpack-dev-server|nuxt|astro)')) -or
            (($_.Name -match 'npm|yarn|pnpm') -and ($_.CommandLine -match 'run\s+dev'))
        }
        foreach ($p in $procs) {
            try {
                Write-Host "Stopping dev process PID $($p.ProcessId) [$($p.Name)] Cmd: $($p.CommandLine)"
                Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
            } catch {}
        }
    } catch {
        Write-Host "Dev process scan failed: $_"
    }
}

Write-Host "Cleanup complete."
