# MediaFlow Proxy - Windows Executable

A high-performance streaming proxy server for media content, built with FastAPI and packaged as a standalone Windows executable.

## 🚀 Quick Start

1. **Download** the latest `mediaflow-proxy-win-v*.zip` from [Releases](../../releases)
2. **Extract** the ZIP file to any folder
3. **Set your API password** (required for security)
4. **Run** the executable

Set your API password
set API_PASSWORD=your_secure_password

Run the server
.\mediaflow-proxy.exe

text

5. **Access** the server at: `http://localhost:8888`

## 📋 System Requirements

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 512MB minimum, 1GB recommended
- **Storage:** 50MB free space
- **Network:** Internet connection for streaming

## ⚙️ Configuration

### Environment Variables

Set these before running the executable:

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PASSWORD` | *(required)* | Authentication password for API access |
| `PORT` | `8888` | Server port number |
| `HOST` | `0.0.0.0` | Server bind address |
| `DISABLE_HTTPS` | `false` | Set to `true` to use HTTP only |
| `DEBUG` | `false` | Enable debug logging |
| `CERT_ADDITIONAL_IPS` | *(none)* | Additional IPs for HTTPS certificate |

### Example Configurations

**Basic Setup:**
set API_PASSWORD=mySecurePassword123
.\mediaflow-proxy.exe

text

**Custom Port:**
set API_PASSWORD=mySecurePassword123
set PORT=9000
.\mediaflow-proxy.exe

text

**HTTP Only Mode:**
set API_PASSWORD=mySecurePassword123
set DISABLE_HTTPS=true
.\mediaflow-proxy.exe

text

**External Access Setup:**
set API_PASSWORD=mySecurePassword123
set CERT_ADDITIONAL_IPS=your.public.ip.address
.\mediaflow-proxy.exe

text

### Using .env File

Create a `.env` file next to the executable:

API_PASSWORD=mySecurePassword123
PORT=8888
DEBUG=false
DISABLE_HTTPS=false

text

## 🌐 Access URLs

After starting, the server will be available at:

- **Local:** `https://127.0.0.1:8888` or `http://127.0.0.1:8888`
- **Network:** `https://your-local-ip:8888` (shown in startup output)
- **API Docs:** `https://127.0.0.1:8888/docs`

## 🔐 HTTPS & SSL Certificates

### Automatic Certificate Generation

The server automatically generates self-signed SSL certificates for HTTPS access. Certificates include:

- `localhost` and `127.0.0.1` (local access)
- Your detected local network IP
- Any IPs specified in `CERT_ADDITIONAL_IPS`

### Certificate Warnings

When using self-signed certificates, browsers will show security warnings:

1. **Chrome/Edge:** Click "Advanced" → "Proceed to [address] (unsafe)"
2. **Firefox:** Click "Advanced" → "Accept the Risk and Continue"
3. **Mobile browsers:** Follow similar steps to accept the certificate

### External Access

For access from outside your network:

1. **Configure router port forwarding:** Forward port 8888 to your PC's local IP
2. **Set your public IP in certificates:**
set CERT_ADDITIONAL_IPS=your.public.ip.address

text
3. **Configure Windows Firewall:**
netsh advfirewall firewall add rule name="MediaFlow" dir=in action=allow protocol=TCP localport=8888

text

## 🛠️ Troubleshooting

### Server Won't Start

**"API_PASSWORD is not set" warning:**
Set the password before running
set API_PASSWORD=yourpassword
.\mediaflow-proxy.exe

text

**Port already in use:**
Use a different port
set PORT=9000
.\mediaflow-proxy.exe

text

### Network Access Issues

**Can't access from other devices:**
1. Check Windows Firewall settings
2. Verify your local IP address in startup output
3. Ensure devices are on the same network

**External access not working:**
1. Configure router port forwarding
2. Check ISP port blocking
3. Verify public IP address
4. Test with HTTP first (`DISABLE_HTTPS=true`)

### Certificate Issues

**Mobile browsers reject HTTPS:**
Regenerate certificates with your network IP
del bin\server.*
.\mediaflow-proxy.exe

text

**Need specific IPs in certificate:**
set CERT_ADDITIONAL_IPS=192.168.1.100,10.0.0.50
.\mediaflow-proxy.exe

text

## 📱 Mobile & Network Usage

### Same Network Access

Other devices on your network can access the server using your local IP:

https://your-local-ip:8888

text

The local IP is displayed in the startup banner.

### Mobile Browser Tips

1. **Accept certificate warnings** when prompted
2. **Try different browsers** if one doesn't work
3. **Use HTTP mode** if HTTPS causes issues:
set DISABLE_HTTPS=true

text

## 🔧 Advanced Configuration

### Debug Mode

Enable detailed logging:
set DEBUG=true
.\mediaflow-proxy.exe

text

### HTTP/2 Support

HTTP/2 is enabled by default over HTTPS. To disable:
set UVICORN_HTTP2=false

text

### Custom Host Binding

Bind to specific interface:
set HOST=192.168.1.100

text

## 📊 Performance Tips

- **Use SSD storage** for better performance
- **Close unnecessary applications** to free up RAM
- **Use wired connection** for stable streaming
- **Enable debug mode** only when troubleshooting

## 🔒 Security Considerations

- **Always set a strong API_PASSWORD**
- **Use HTTPS when possible**
- **Don't expose to internet without proper security**
- **Keep the executable updated**
- **Monitor access logs in debug mode**

## 📄 File Structure

mediaflow-proxy/
├── mediaflow-proxy.exe # Main executable
├── .env # Optional configuration file
└── bin/ # Auto-generated certificates
├── server.pem # SSL certificate
└── server.key # SSL private key

text

## 🆘 Support

If you encounter issues:

1. **Check this README** for common solutions
2. **Enable debug mode** to see detailed logs
3. **Report issues** with full startup output
4. **Include your configuration** (without passwords)

## 📝 License

[Include your license information here]

---

**Made with ❤️ using Python, FastAPI, and PyIns
