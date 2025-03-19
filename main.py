import prepare_text as pt
import text_generate as tg

image_path = 'images/report.webp'

extracted_text = pt.extract_text(image_path)

data = pt.process_report_data(extracted_text)

final_data = pt.add_reference_data(data)

explaination = tg.generate_explanation(final_data)

tg.save_to_file(explaination, "explainations/explaination_before_cleanning.md")

explaination = tg.clean_response(explaination)

tg.save_to_file(explaination, "explainations/explaination_after_cleanning.md")