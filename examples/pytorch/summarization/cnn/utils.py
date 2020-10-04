# import torchtext.vocab as vocab
from graph4nlp.pytorch.modules.utils.vocab_utils import Vocab
import torch, logging


def get_glove_weights(glove, vocabulary: Vocab, dim=300):


    vocab_size = vocabulary.get_vocab_size()
    weight = torch.randn(vocab_size, dim)
    cnt = 0
    all = 0
    for i, word in enumerate(vocabulary.index2word):
        all += 1
        glove_index = glove.stoi.get(word)
        if glove_index is not None:
            cnt += 1
        glove_rep = glove.get_vecs_by_tokens(word)
        weight[i, :] = glove_rep
    print("Hit ratio: {:.3f}".format(cnt/all))
    return weight


def get_log(log_file):
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger



def wordid2str(word_ids, vocab: Vocab):
    ret = []
    assert len(word_ids.shape) == 2, print(word_ids.shape)
    for i in range(word_ids.shape[0]):
        id_list = word_ids[i, :]
        ret_inst = []
        for j in range(id_list.shape[0]):
            if id_list[j] == vocab.EOS:
                break
            token = vocab.getWord(id_list[j])
            ret_inst.append(token)
        ret.append(" ".join(ret_inst))
    return ret