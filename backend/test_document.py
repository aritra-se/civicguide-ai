from app.agents.document_agent import create_document_agent
import io

def test_document_agent():
    print("Initializing Document Agent...")
    agent = create_document_agent()
    
    # Create a tiny 1x1 white PNG image in memory for testing multimodal input
    dummy_png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc````\x00\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    
    required_checklist = ["Identity proof", "Income certificate"]
    
    print("Sending dummy document image to Document Agent...")
    try:
        response_json = agent.analyze_document(dummy_png_bytes, "image/png", required_checklist)
        print("--- DOCUMENT ANALYSIS RESPONSE ---")
        print(response_json)
    except Exception as e:
        print(f"Error during document analysis: {e}")

if __name__ == "__main__":
    test_document_agent()