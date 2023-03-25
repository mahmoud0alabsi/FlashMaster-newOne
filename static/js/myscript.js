(function ($) {

    document.addEventListener("DOMContentLoaded", function(event) {
        window.onload = function () { 
            const flashcard = document.querySelector("#flashcard"); 
            flashcard.addEventListener("click", function () { 
              flashcard.classList.toggle("flipped"); 
            }); 
           
          // pass ans receive ques_list 
            const ques_list = document.getElementById("ques_list").innerHTML; 
            const ans_list = document.getElementById("ans_list").innerHTML; 
           
            const ques_item = ques_list.split("$%$"); 
            const ans_item = ans_list.split("$%$"); 
            console.log(ques_item); 
            console.log(ans_item); 
           
            const questions = []; 
            for (let i = 0; i < ques_item.length; i++){ 
              if(ques_item[i] != "" && ans_item[i] != ""){ 
                questions.push({ 
                  key:   ques_item[i], 
                  value: ans_item[i] 
                }) 
              }; 
              //questions[ques_item[i]] = ans_item[i]; 
            }; 
           
            console.log(questions[0]); 
          //--------------- 
           
           
            let currentIndex = 0; 
           
            const prevButton = document.getElementById("prev"); 
            const nextButton = document.getElementById("next"); 
           
            const txtBUtton = document.getElementById("btn_txt"); 
            const pdfBUtton = document.getElementById("btn_pdf"); 
           
              //--------------CARDS COUNTER----------------//  
            var cards_no = ques_item.length;  
             
            document.getElementById("cards_no").innerHTML = cards_no; 
              //--------------CARDS COUNTER----------------//  
           
            const questionElement = document.querySelector("#front"); 
            const answerElement = document.querySelector("#back"); 
           
            prevButton.addEventListener("click", function () { 
              if (flashcard.classList.contains("flipped")) { 
                flashcard.classList.remove("flipped"); 
              } 
              currentIndex = (currentIndex - 1 + questions.length) % questions.length; 
              updateFlashcard(); 
            }); 
           
            nextButton.addEventListener("click", function () { 
              if (flashcard.classList.contains("flipped")) { 
                flashcard.classList.remove("flipped"); 
              } 
           
              currentIndex = (currentIndex + 1) % questions.length; 
              updateFlashcard(); 
            }); 
           
            function updateFlashcard() { 
              questionElement.innerText = questions[currentIndex].key; 
              answerElement.innerText = questions[currentIndex].value; 
            } 
           
            updateFlashcard(); 
          }; 
           
           
        });

    
      })(window.jQuery);
      