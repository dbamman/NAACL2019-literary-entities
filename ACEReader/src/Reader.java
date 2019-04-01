import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.ie.machinereading.domains.ace.AceReader;
import edu.stanford.nlp.ie.machinereading.structure.EntityMention;
import edu.stanford.nlp.ie.machinereading.structure.MachineReadingAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;


public class Reader {

	public static void main(String[] args) throws IOException {

		String acePath = args[0];
		String outputDir = args[1];

		File f = new File(outputDir);
		f.mkdirs();
		
		Properties props = new Properties();
		props.put("annotators", "tokenize, ssplit");

		AceReader r = new AceReader(new StanfordCoreNLP(props, false), false);
		Annotation a = r.parse(acePath);
		List<CoreMap> sentences = a.get(SentencesAnnotation.class);

		String docid = null;
		PrintStream os = null;

		for (int cm_indx = 0; cm_indx < sentences.size(); cm_indx++) {
			CoreMap sentence = sentences.get(cm_indx);

			String myDocid = sentence
					.get(CoreAnnotations.DocIDAnnotation.class);
			if (docid == null || !myDocid.equals(docid)) {
				if (os != null) {
					os.close();
				}
				docid = myDocid;
				os = new PrintStream(new FileOutputStream(outputDir
						+ File.separator + docid + ".txt"));
			}

			for (int ci = 0; ci < sentence.get(TokensAnnotation.class).size(); ci++) {

				CoreLabel token = sentence.get(TokensAnnotation.class).get(ci);
				os.printf("%s", token.word());
				if (ci < sentence.get(TokensAnnotation.class).size() - 1) {
					os.print(" ");
				} else {
					os.print("\n");
				}

			}
			List<EntityMention> mentions = sentence
					.get(MachineReadingAnnotations.EntityMentionsAnnotation.class);
			if (mentions != null) {
				for (int ei = 0; ei < mentions.size(); ei++) {
					EntityMention mention = mentions.get(ei);
					os.printf("%s %s %s %s %s %s %s", mention.getType(),
							mention.getSubType(), mention.getMentionType(),
							mention.getExtentTokenStart(),
							mention.getExtentTokenEnd(),
							mention.getHeadTokenStart(),
							mention.getHeadTokenEnd());
					if (ei < mentions.size() - 1) {
						os.print("|");
					} else {
						os.print("\n");
					}
				}
			} else {
				os.print("\n");
			}

			os.print("\n");
		}
		if (os != null) {
			os.close();
		}

	}

}
