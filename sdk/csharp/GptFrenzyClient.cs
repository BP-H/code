using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

public class GptFrenzyClient
{
    private readonly HttpClient _http;
    private readonly string _base;

    public GptFrenzyClient(string baseUrl = "http://localhost:8000")
    {
        _http = new HttpClient();
        _base = baseUrl.TrimEnd('/');
    }

    public async Task<string> Chat(string character, string message)
    {
        var payload = JsonConvert.SerializeObject(new { character, message });
        var resp = await _http.PostAsync($"{_base}/chat",
            new StringContent(payload, Encoding.UTF8, "application/json"));
        resp.EnsureSuccessStatusCode();
        dynamic body = JsonConvert.DeserializeObject(await resp.Content.ReadAsStringAsync());
        return (string)body.reply;
    }

    public async Task<dynamic> Manifest()
    {
        var resp = await _http.GetAsync($"{_base}/manifest");
        resp.EnsureSuccessStatusCode();
        return JsonConvert.DeserializeObject(await resp.Content.ReadAsStringAsync());
    }
}
