import csv

class HtmlGenerator():
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
    
    @staticmethod
    def generate_description(description_text):
        if description_text.strip() == "":
            return ""
        else:
            return f"""\n\t\t<h1>Description</h1>
            \t<span>{description_text}</span>\n
            """.rstrip()
    
    @staticmethod
    def generate_ul_contents(domains):
        ul_contents = ""
        for d in domains:
            if d.strip() != "":
                ul_contents += f"\n\t\t\t\t<li>{d}</li>"
        return ul_contents
            
    @staticmethod
    def generate_html_content(title, description, ul_contents):

        content = f"""
        <html>
        \t<head>
            \t<title>{title}</title>
        \t</head>
        \t<body>{description}
            \t<h1>Domains</h1>
            \t\t<ul>{ul_contents}
            \t\t</ul>
        \t</body>\n</html>
        """

        return content

    def generate_html(self):
        input_file = self.input_file
        output_file = self.output_file

        with open(output_file, "w") as f:
            f.write("assessment_id,html\n")

        with open(input_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                id = row[0]
                title = row[1]
                description_text = row[2]
                description = self.generate_description(description_text)
                
                domains = [row[3], row[4], row[5]]
                ul_contents = self.generate_ul_contents(domains)
                
                content = self.generate_html_content(title, description, ul_contents)
                
                with open(output_file, "a+") as f:
                    f.write(",".join([id, f"\"{content.strip()}\"\n"]))


if  __name__ == "__main__":
    html_generator = HtmlGenerator(input_file = "../data/assessment.csv", output_file="../data/output_assessment.csv")
    html_generator.generate_html()
