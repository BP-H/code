using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.IO;
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

    public async IAsyncEnumerable<string> ChatStream(string character, string message)
    {
        var payload = JsonConvert.SerializeObject(new { character, message });
        using var req = new HttpRequestMessage(HttpMethod.Post, $"{_base}/chat/stream")
        {
            Content = new StringContent(payload, Encoding.UTF8, "application/json")
        };
        var resp = await _http.SendAsync(req, HttpCompletionOption.ResponseHeadersRead);
        resp.EnsureSuccessStatusCode();
        var stream = await resp.Content.ReadAsStreamAsync();
        using var reader = new StreamReader(stream);
        while (true)
        {
            var line = await reader.ReadLineAsync();
            if (line == null)
                yield break;
            if (line.StartsWith("data: "))
                yield return line.Substring(6);
        }
    }

    public async Task<dynamic> Manifest()
    {
        var resp = await _http.GetAsync($"{_base}/manifest");
        resp.EnsureSuccessStatusCode();
        return JsonConvert.DeserializeObject(await resp.Content.ReadAsStringAsync());
    }
}
