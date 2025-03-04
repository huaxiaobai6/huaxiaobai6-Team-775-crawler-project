import java.util.Arrays;
import java.util.List;

public class SeedURLManager {
    public static List<String> getSeedUrls() {
        // 从配置文件/数据库读取种子URL
        return Arrays.asList(
                "https://example.com",
                "https://example.org"
        );
    }
}