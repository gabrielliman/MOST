#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h> 
#include <string>
#include <vector>

namespace py = pybind11;

class SentenceEmbedding {
public:
    SentenceEmbedding(const std::string& sentence, const std::vector<float>& embeddings)
        : sentence_(sentence), embeddings_(embeddings) {}

    std::string get_sentence() const {
        return sentence_;
    }

    py::array_t<float> get_embeddings() const {
        return py::array_t<float>(embeddings_.size(), embeddings_.data());
    }

private:
    std::string sentence_;
    std::vector<float> embeddings_;
};

PYBIND11_MODULE(sentence_embedding, m) {
    py::class_<SentenceEmbedding>(m, "SentenceEmbedding")
        .def(py::init<const std::string&, const std::vector<float>&>())
        .def("get_sentence", &SentenceEmbedding::get_sentence)
        .def("get_embeddings", &SentenceEmbedding::get_embeddings);
}
