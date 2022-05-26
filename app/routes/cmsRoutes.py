from flask import Blueprint
from flask import render_template
from flask_jwt_extended import jwt_required, current_user
import jwt
from ..models.postModel import Post
from ..models.publicationModel import Publication
from ..models.projectModel import Project
from ..models.memberModel import Member
from ..models.galleryModel import Gallery
from ..models.commentModel import Comment
from ..models.productModel import Product
from ..models.paymentModel import Payment
from ..controllers import menuController


cmsRoutes = Blueprint('cmsRoutes', __name__)

@cmsRoutes.route('/cms/login', methods=['GET'])
def login():
    return render_template('cms/login.html')

@cmsRoutes.route('/cms', methods=['GET'])
@jwt_required()
def getAll():
    posts=Post.findMany({'active': True})
    postN = len(posts)

    publications=Publication.findMany({'active': True})
    publicationN = len(publications)

    projects=Project.findMany({'active': True})
    projectN=len(projects)

    members=Member.findMany({'active': True})
    memberN=len(members)

    galleries=Gallery.findMany({'active': True})
    galleryN=len(galleries)

    comments=Comment.findMany({'active': True})
    commentN=len(comments)
    return render_template('cms/index.html', 
                            posts=posts[:5], 
                            postN=postN, 
                            publications=publications[:5], 
                            publicationN=publicationN,
                            projects=projects[:5],
                            projectN=projectN,
                            members=members,
                            memberN=memberN,
                            galleries=galleries,
                            galleryN=galleryN,
                            comments=comments,
                            commentN=commentN,
                            user=current_user,
                            title='Dashboard')


#######################
####member routes######
@cmsRoutes.route('/cms/members', methods=['GET'])
@jwt_required()
def members():
    members=Member.findMany({})
    return render_template('cms/members.html', members=members, user=current_user, title='Team Members')


@cmsRoutes.route('/cms/member', methods=['GET'])
@jwt_required()
def createMember():
    return render_template('cms/addEditMember.html', user=current_user, title='Add Team Member')


@cmsRoutes.route('/cms/member/<string:memberId>', methods=['GET'])
@jwt_required()
def editMember(memberId):
    member = Member.findOne({'_id': memberId})
    return render_template('cms/addEditMember.html', member = member, user=current_user, title='Edit Team Member')
####end of member routes#####
#############################


##############################
#####post routes##############
@cmsRoutes.route('/cms/posts', methods=['GET'])
@jwt_required()
def posts():
    posts=Post.findMany({ '$query': {}, '$orderby': { '_createdAt' : -1 } }, limit=10)
    return render_template('cms/posts.html', posts=posts, user=current_user, title='All Posts')


@cmsRoutes.route('/cms/post', methods=['GET'])
@jwt_required()
def createPost():
    categories=Post.Schema['category']['validators'][1][1]
    return render_template('cms/addEditPost.html', user=current_user, categories=categories, title='Add Post')


@cmsRoutes.route('/cms/post/<string:postId>', methods=['GET'])
@jwt_required()
def updatePost(postId):
    post = Post.findOne({'_id': postId})
    categories=Post.Schema['category']['validators'][1][1]
    return render_template('cms/addEditPost.html', post=post, user=current_user, categories=categories, title='Edit Post')
#####end of post routes#######
#############################

################################
######publication routes###########
@cmsRoutes.route('/cms/publications', methods=['GET'])
@jwt_required()
def publications():
    publications=Publication.findMany({ '$query': {}, '$orderby': { '_createdAt' : -1 } }, limit=10)
    return render_template('cms/publications.html', publications=publications, user=current_user, title='All Publications')


@cmsRoutes.route('/cms/publication', methods=['GET'])
@jwt_required()
def createPublications():
    return render_template('cms/addEditPublication.html', user=current_user, title='Add Publication')


@cmsRoutes.route('/cms/publication/<string:publicationId>', methods=['GET'])
@jwt_required()
def updatePublications(publicationId):
    publication=Publication.findOne({'_id': publicationId})
    return render_template('cms/addEditPublication.html', publication=publication, user=current_user, title='Edit Publication')


#####end of publication routes#########
#######################################

######################################
####project routes####################

@cmsRoutes.route('/cms/projects', methods=['GET'])
@jwt_required()
def projects():
    projects=Project.findMany({ '$query': {}, '$orderby': { '_createdAt' : -1 } }, limit=10)
    return render_template('cms/projects.html', projects=projects, user=current_user, title='All Projects')


@cmsRoutes.route('/cms/project', methods=['GET'])
@jwt_required()
def createProject():
    return render_template('cms/addEditProject.html', user=current_user, title='Add Project')


@cmsRoutes.route('/cms/project/<string:projectId>', methods=['GET'])
@jwt_required()
def editProject(projectId):
    project = Project.findOne({'_id': projectId})
    return render_template('cms/addEditProject.html', project=project, user=current_user, title='Edit Project')

###end of project routes##############
######################################


######################################
########gallery routes################
@cmsRoutes.route('/cms/galleries', methods=['GET'])
@jwt_required()
def galleries():
    galleries=Gallery.findMany({ '$query': {}, '$orderby': { '_createdAt' : -1 } }, limit=10)
    return render_template('cms/galleries.html', galleries=galleries, user=current_user, title='All Galleries')


@cmsRoutes.route('/cms/gallery', methods=['GET'])
@jwt_required()
def createGallery():
    return render_template('cms/addEditGallery.html', user=current_user, title='Add Gallery')


@cmsRoutes.route('/cms/gallery/<string:galleryId>', methods=['GET'])
@jwt_required()
def updateGallery(galleryId):
    gallery=Gallery.findOne({'_id': galleryId})
    return render_template('cms/addEditGallery.html', gallery=gallery, user=current_user, title='Edit Gallery')

########end of gallery routes#########
######################################


#############################################
###########market routes####################

@cmsRoutes.route('/cms/products', methods=['GET'])
@jwt_required()
def products():
    products=Product.findMany({ '$query': {}, '$orderby': { '_createdAt' : -1 } }, limit=10)
    return render_template('cms/products.html', products=products, user=current_user, title='All Products')


@cmsRoutes.route('/cms/product', methods=['GET'])
@jwt_required()
def createProduct():
    return render_template('cms/addEditProduct.html', user=current_user, title='Add Product')


@cmsRoutes.route('/cms/product/<string:productId>', methods=['GET'])
@jwt_required()
def updateProduct(productId):
    product=Product.findOne({'_id': productId})
    return render_template('cms/addEditProduct.html', product=product, user=current_user, title='Edit Product')


@cmsRoutes.route('/cms/payments', methods=['GET'])
@jwt_required()
def payments():
    payments = Payment.findMany({ '$query': {}, '$orderby': { '_createdAt' : -1 } }, limit=50)
    return render_template('cms/payments.html', payments=payments, user=current_user, title='Payments archive')


##########end of market routes################
##############################################


##########################################
##########menu builder####################
@cmsRoutes.route('/cms/menu', methods=['GET'])
@jwt_required()
def menu():
    return render_template('cms/menuBuilder.html', user=current_user, title='Menu Builder')

############end of menu builder############
###########################################

###########################################
########settings routes###################

@cmsRoutes.route('/cms/settings', methods=['GET'])
@jwt_required()
def settings():
    return render_template('cms/settings.html', user=current_user, title='Settings')
######end of settings routes###############
###########################################




