import Docker from 'dockerode';

const docker = new Docker({ socketPath: '/var/run/docker.sock' });

export async function listContainers() {
    try {
        const containers = await docker.listContainers({ all: true });
        return containers.map(c => ({
            id: c.Id.substring(0, 12),
            name: c.Names[0]?.replace('/', '') || 'unnamed',
            image: c.Image,
            state: c.State,
            status: c.Status,
            created: c.Created,
            ports: c.Ports?.map(p => `${p.PublicPort || '?'}:${p.PrivatePort}`).join(', ') || '-'
        }));
    } catch (error) {
        console.error('Docker listContainers error:', error);
        throw error;
    }
}

export async function startContainer(containerId) {
    const container = docker.getContainer(containerId);
    await container.start();
    return { success: true, message: `Container ${containerId} started` };
}

export async function stopContainer(containerId) {
    const container = docker.getContainer(containerId);
    await container.stop();
    return { success: true, message: `Container ${containerId} stopped` };
}

export async function restartContainer(containerId) {
    const container = docker.getContainer(containerId);
    await container.restart();
    return { success: true, message: `Container ${containerId} restarted` };
}

export async function removeContainer(containerId, force = false) {
    const container = docker.getContainer(containerId);
    await container.remove({ force });
    return { success: true, message: `Container ${containerId} removed` };
}

export async function getContainerLogs(containerId, tail = 100) {
    const container = docker.getContainer(containerId);
    const logs = await container.logs({ stdout: true, stderr: true, tail });
    return logs.toString('utf8');
}

export default docker;
