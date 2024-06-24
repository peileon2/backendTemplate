import base64
import json


def decode_jwt_payload(jwt_token: str) -> dict:
    try:
        # 分割 JWT 字符串
        header, payload, _ = jwt_token.split(".")

        # Base64 解码 header 和 payload
        decoded_header = base64.b64decode(header + "=" * (-len(header) % 4)).decode(
            "utf-8"
        )
        decoded_payload = base64.b64decode(payload + "=" * (-len(payload) % 4)).decode(
            "utf-8"
        )

        # 将解码后的 JSON 字符串转换为 Python 字典
        payload_dict = json.loads(decoded_payload)

        return payload_dict
    except Exception as e:
        print(f"Error decoding JWT payload: {e}")
        return {}


# 假设您有一个 JWT
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYzQxMjkzYi0wZTA4LTRmNmItOTdiYS0wMDgxZmE3N2M3YjkiLCJhdWQiOlsiZmFzdGFwaS11c2VyczphdXRoIl0sImV4cCI6MTcxOTIyNDYwNH0.6KiK8o2KeReww43f_gy9sClwBJPdZx-zd4315ymJi34"

# 解析 JWT 的 payload
payload = decode_jwt_payload(jwt_token)
print(payload)
